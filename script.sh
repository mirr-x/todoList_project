#!/bin/bash

# Define the file path to store the Virtual_Environment name
File_Path="virtual_env.txt"

# Setup Virtual Environment
echo -e "\e[33mEnter your Virtual Environment :\e[0m"
read Virtual_Environment

if grep -q "$Virtual_Environment :" "$File_Path"; then
    
    echo -e "\e[32mVirtual Environment Is Exists.\e[0m"
    # Perform other operations
    
    source $Virtual_Environment/bin/activate
    # اقرأ المسار من الملف واستخرج المسار فقط وضعه في المتغير project_path
    project_path=$(cut -d':' -f2 $File_Path)
    
    # تنظيف المسار من الفراغات الزائدة
    project_path=$(echo $project_path | tr -d '[:space:]')
    
    cd $project_path
    
    while true; do
        options=("1 - Run Server ?" "2 - Create App ?" "3 - Makemigrations & Migrate ?" "4 - Collect Static Files ?" "5 - Exit")
        select choice in "${options[@]}"
        do
            case $choice in
                "1 - Run Server ?")
                    python manage.py runserver
                    break
                ;;
                "2 - Create App ?")
                    echo -e "\e[33mCreate Your App :\e[0m"
                    read Your_App
                    python manage.py startapp $Your_App
                    python manage.py runserver
                    break
                ;;
                "3 - Makemigrations & Migrate ?")
                    python manage.py makemigrations && python manage.py migrate
                    python manage.py runserver
                    break
                ;;
                "4 - Collect Static Files ?")
                    python manage.py collectstatic
                    python manage.py runserver
                    break
                ;;
                "5 - Exit")
                    deactivate
                    echo "Exiting..."
                    exit
                ;;
                *)
                    echo -e "\e[31mInvalid Choice, Please Select A Valid Option !\e[0m"
                ;;
            esac
        done
    done
else
    echo -e "\e[31mVirtual Environment Is Not Exists.\e[0m"
    
    python -m venv $Virtual_Environment
    source $Virtual_Environment/bin/activate
    cd $Virtual_Environment
    
    # Install Django
    python -m pip install Django
    
    # Create Django Project
    echo -e "\e[33mEnter your project name :\e[0m"
    read your_project
    django-admin startproject $your_project
    
    cd $your_project && current_path=$(pwd) && cd ..
    
    cd .. && echo "$Virtual_Environment : $current_path" >> "$File_Path" && cd ./$Virtual_Environment/$your_project/
    
    python manage.py makemigrations && python manage.py migrate
    
    # Create Super User
    echo -e "\e[33mEnter your Email :\e[0m"
    read Email
    
    python manage.py createsuperuser --email $Email --username $Email
    
    python manage.py runserver
fi
