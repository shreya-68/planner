#first check if the machine has python or not if not then install it;

var=`python --version`; 
actualversion="Python 2.7"
#this will give you the version and will compare with the ssuitable version requires for installation of Django
if [ var>=actualversion ]
   then
   echo "your version is quit old"
fi
