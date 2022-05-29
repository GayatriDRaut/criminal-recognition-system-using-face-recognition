from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
import face_recognition
from PIL import Image, ImageDraw
import numpy as np
import cv2
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from django.contrib.auth import logout
from .models import User, Person, ThiefLocation


class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
      file_serializer.save()
      return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# view for index
def index(request):
    return render(request, 'session/login.html')


#view for log in
def login(request):
    if((User.objects.filter(email=request.POST['login_email']).exists())):
        user = User.objects.filter(email=request.POST['login_email'])[0]
        if ((request.POST['login_password']== user.password)):
            request.session['id'] = user.id
            request.session['name'] = user.first_name
            request.session['surname'] = user.last_name
            messages.add_message(request,messages.INFO,'Welcome to criminal detection system '+ user.first_name+' '+user.last_name)
            return redirect(success)
        else:
            messages.error(request, 'Oops, Wrong password, please try a diffrerent one')
            return redirect('/')
    else:
        messages.error(request, 'Oops, That police ID do not exist')
        return redirect('/')


#view for log out
def logOut(request):
    logout(request)
    messages.add_message(request,messages.INFO,"Successfully logged out")
    return redirect(index)


# view to add crimina
def addCitizen(request):
   return render(request, 'home/add_citizen.html')


# view to add save citizen
def saveCitizen(request):
    if request.method == 'POST':
        citizen=Person.objects.filter(aadhar_no=request.POST["aadhar_no"])
        if citizen.exists():
            messages.error(request,"Citizen with that Aadhar Number already exists")
            return redirect(addCitizen)
        else:
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            person = Person.objects.create(
                name=request.POST["name"],
                aadhar_no=request.POST["aadhar_no"],
                address=request.POST["address"],
                picture=uploaded_file_url[1:],
                status="Free"
            )
            person.save()
            messages.add_message(request, messages.INFO, "Citizen successfully added")
            return redirect(viewCitizens)


# view to get citizen(criminal) details
def viewCitizens(request):
    citizens=Person.objects.all();
    context={
        "citizens":citizens
    }
    return render(request,'home/view_citizens.html',context)


#view to set criminal status to wanted
def wantedCitizen(request, citizen_id):
    wanted = Person.objects.filter(pk=citizen_id).update(status='Wanted')
    if (wanted):
        messages.add_message(request,messages.INFO,"User successfully changed status to wanted")
    else:
        messages.error(request,"Failed to change the status of the citizen")
    return redirect(viewCitizens)

#view to set criminal status to free
def freeCitizen(request, citizen_id):
    free = Person.objects.filter(pk=citizen_id).update(status='Free')
    if (free):
        messages.add_message(request,messages.INFO,"User successfully changed status to Found and Free from Search")
    else:
        messages.error(request,"Failed to change the status of the citizen")
    return redirect(viewCitizens)


def spottedCriminals(request):
    thiefs=ThiefLocation.objects.filter(status="Wanted")
    context={
        'thiefs':thiefs
    }
    return render(request,'home/spotted_thiefs.html',context)


def foundThief(request,thief_id):
    free = ThiefLocation.objects.filter(pk=thief_id)
    freectzn = ThiefLocation.objects.filter(aadhar_no=free.get().aadhar_no).update(status='Found')
    if(freectzn):
        thief = ThiefLocation.objects.filter(pk=thief_id)
        free = Person.objects.filter(aadhar_no=thief.get().aadhar_no).update(status='Found')
        if(free):
            messages.add_message(request,messages.INFO,"Thief updated to found, congratulations")
        else:
            messages.error(request,"Failed to update thief status")
    return redirect(spottedCriminals)





def success(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        "user": user
    }
    return render(request, 'home/welcome.html', context)


# view to detect and recognise faces
def detectImage(request):
    # function to detect faces and draw a rectangle around the faces
    # with correct face label

    if request.method == 'POST' and request.FILES['image']:
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

    # get the criminal id, name, images from the database
    images=[]
    encodings=[]
    names=[]
    files=[]

    prsn=Person.objects.all()
    for criminal in prsn:
        images.append(criminal.name+'_image')
        encodings.append(criminal.name+'_face_encoding')
        files.append(criminal.picture)
        names.append(criminal.name+ ' '+ criminal.address)

    
    for i in range(0,len(images)):
        images[i]=face_recognition.load_image_file(files[i])
        encodings[i]=face_recognition.face_encodings(images[i])[0]




    # encoding the faces of the criminals in the database 
    # creating array of their names
    known_face_encodings = encodings
    known_face_names = names

    # loading the image that is coming from the front end
    unknown_image = face_recognition.load_image_file(uploaded_file_url[1:])

    # finding face locations and encoding of that image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    # converting the image to PIL format
    pil_image = Image.fromarray(unknown_image)
    #Draw a rectangle over the face
    draw = ImageDraw.Draw(pil_image)

    # run a for loop to find if faces in the input image matches to that 
    # of our encoding present in the DB
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # compare the face to the criminals present
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # find distance w.r.t to the faces of criminals present in the DB
        # take the minimum distance
        # see if it matches the faces
        # if matches update the name variable to the respective criminal name
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]


        # with pollow module draw a rectangle around the face
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # put a label of name of the person below
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    # Remove the drawing library from memory 
    del draw

    # display the image 
    pil_image.show()
    return redirect('/success')



# View to detect criminals using webcam
def detectWithWebcam(request):
    # Accessing the deafult camera of the system
    video_capture = cv2.VideoCapture(0)

    # Loading faces from DB with their data.
    images=[]
    encodings=[]
    names=[]
    files=[]
    nationalIds=[]

    prsn=Person.objects.all()
    for criminal in prsn:
        images.append(criminal.name+'_image')
        encodings.append(criminal.name+'_face_encoding')
        files.append(criminal.picture)
        names.append('Name: '+criminal.name+ ', AadharNo: '+ criminal.aadhar_no+', Address '+criminal.address)
        nationalIds.append(criminal.aadhar_no)

    #finding encoding of the criminals
    for i in range(0,len(images)):
        images[i]=face_recognition.load_image_file(files[i])
        encodings[i]=face_recognition.face_encodings(images[i])[0]


    # Encoding of faces and their respective ids and names
    known_face_encodings = encodings
    known_face_names = names
    n_id = nationalIds



    while True:
        # Reading a single frame of the video
        ret, frame = video_capture.read()

        # converting color channel from RBG to BRG 
        rgb_frame = frame[:, :, ::-1]

        # Finding all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Run a loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
          
           # checking if the faces in the frame matches to that from our DB
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"

            # finding distance of the faces in the frame to that from our DB
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            #if it matches with the one with minimum distance then print their name on the frame
            if matches[best_match_index]:
                ntnl_id = n_id[best_match_index]
                person = Person.objects.filter(aadhar_no=ntnl_id)
                name = known_face_names[best_match_index]+', Status: '+person.get().status


                # if the face is of a wanted criminal then add it to ThiefLocation list
                if(not(person.get().status=='Wanted')):
                    thief = ThiefLocation.objects.create(
                        name=person.get().name,
                        aadhar_no=person.get().aadhar_no,
                        address=person.get().address,
                        picture=person.get().picture,
                        status='Wanted',
                        latitude='25.3176° N',
                        longitude='82.9739° E'
                    )
                    thief.save()



            # Drawing Rectangular box around the face(s)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Put a label of their name 
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Now display their faces with frames
        cv2.imshow('Video', frame)

        # To quit the webcam detect enter 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Now release the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    return redirect('/success')



