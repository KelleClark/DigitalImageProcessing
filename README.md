---
author:
- 'Elizabeth Chilcoat, Kelle Clark, Michael Heath'
title: Image Browser Project Documentation
---

Usage and System Dependencies
=============================

Dependencies
------------

The user should check to see if the following libraries are installed or
do a batch install with

    pip install -r requirements.txt 

The libraries and versions used by the team include:

``` {.bash language="bash"}
filetype v 1.0.7
opencv_python_headless v 4.4.0.40
numpy v 1.19.1
Pillow v 7.2.0
```

If only one or two libraries are missing, they can be added with:

    pip install filetype\\
    pip3 install filetype\\

    pip install opencv-contrib-python\\
    pip3 install opencv-contrib-python\\

    pip install numpy\\
    pip3 install numpy\\

    pip install pillow\\
    pip3 install pillow\\

Usage
-----

To run in the command line:

``` {.bash language="bash"}
>python image-browser.py [params] dir  
  
```

where optional parameters are:

      >python image_browser.py -r numrows -c numcols dir

and

``` {.bash language="bash"}
image_browser  name of the executable
   numrows  maximum number of rows in the display window
   (default: 720)\\
   numcols  maximum number of columns in the display window
   (default: 1080)
   dir  input directory
```

![\"Command line instructions for running the
program\"](images/runningImageBrowser.PNG){#Fig:CreateCourse
width=".95\\textwidth"}

User Requirements Log
=====================

The design, implementation and testing of the system are based on
satisfying the following stated user requirements.

Requirements regarding reading all images in given directory/subdirectory:
--------------------------------------------------------------------------

1.  Given a directory, display each picture in the directory as well as
    in its subdirectories.

2.  The system should be able to access all files which are stored in a
    hierarchically-structured directory tree. Let us call the top-level
    directory as dirA. This directory will contain some images as well
    as other (sub)directories. Let us call these (sub)directories as
    dirA1, dirA2, and so on. Each of these subdirectories in turn will
    contain some images and may contain other (sub)directories. This
    (sub)directory structure may extend to an arbitrary number of
    levels.

3.  The GUI should enable browsing of images which are stored in a
    hierarchically structured directory tree in depth-first order.

Requirements regarding execution, input and messages:
-----------------------------------------------------

1.  The system should be invoked using the following command:\

    ``` {.bash language="bash"}
    >python image_browser.py -r numrows -c numcols dir
    ```

    where

    ``` {.bash language="bash"}
    image_browser  name of the executable
       numrows  maximum number of rows in the display window
       (default: 720)\\
       numcols  maximum number of columns in the display window
       (default: 1080)
       dir  input directory
    ```

2.  The system should provide help to the user on the command line
    with:\

    ``` {.bash language="bash"}
    >python image-browser.py -help
    ```

    When invoked with -h option, it should display help similar to the
    following appropriate for MacOS and exit. If running on Windows, the
    default values need to be modified.

        Image Browser v1.0
        Usage: >python image-browser.py [params] dir        

        --? , -h, --help, --usage (value:true)
            print this message                      
        --c         , --cols (value:1280)
            Max number of columns on screen             
        --r         , --rows (value:720)
            Max number of rows on screen                    
        dir 
            Directory that contains the pictures to browse 

    The parameters prefixed with the - (dash) are optional. You are free
    to use long parameter names such as --rows for -r

Requirements regarding the GUI functionality:
---------------------------------------------

1.  Include a simple Graphical User Interface, GUI, for browsing images.

2.  The valid inputs from user will be: space bar or n (for next image),
    p (for previous image), and q (to stop the program).

3.  The image information (name, size) should be displayed in the
    console window.

4.  In addition to displaying images, the GUI should also display
    meta-data associated with the images. Available meta-data may
    include image file name, file path, image file type, image size
    (number of rows and columns), number of pixels (number of rows
    $\times$ number of columns), and image file size in bytes.

5.  The system will ensure that the image fits within specified pixel
    dimensions while preserving aspect ratio for user's OS.

6.  The system should make sure that the image completely fits in the
    display window. Note that this can be achieved by using the Affine
    transformation function of OpenCV that will preserve the aspect
    ratio.

Requirements regarding exception handling:
------------------------------------------

1.  Any exceptions should be handled by the system, so that the program
    will always either execute as expected or exit. An error message of
    why the system exited is optional.

Requirement to use OpenCV library:
----------------------------------

1.  The project should demonstrate the team's level of familiar with
    OpenCV, specifically with the tasks of

    1.  reading an image

    2.  displaying an image

    3.  allowing user interactivity with display window

    4.  performing Affine transforms on the image

Software Model, Development Methodology
=======================================

The team used the Iterative Software Engineering model with some
features of the Integrate and Configure Model to perform the tasks of
specification, development and testing. The team of 3 found it easy to
communicate frequently through the Team's channel on Microsoft Team, all
members were involved in understanding the stated user requirements,
developing the implied system requirements, provided short feedback on
progress, and worked together on coding and the architecture of the
system through shared files. A workable piece of code was generated with
the focus of meeting one function, and each of these sprints were
finished in less than a day. These practices are in line with the Agile
manifesto, but the team also relied heavily on scripts and libraries
found in research to use in the development. For instance the initial
requirement that the system be implemented using C++ was modified when
the team found that their skill level was not appropriate at the time in
this language and the processes involved in running C++ code. Research
revealed support for OpenCV in Python, so the team changed the language
of the system to Python given that the requirement could be modified to
allow for any language except Matlab. The following represents the
general architecture of the system which includes both implemented
functionality and proposed future functionality:

![\"Command line instructions for running the
program\"](images/imagebrowserarch.png){#Fig:CreateCourse
width=".95\\textwidth"}

Testing the System
==================

A directory was created for testing that included empty files, files of
varying types (HTML, PDF, Word) and images stored in different formats:

![\"Command line instructions for running the
program\"](images/TestFileHierarchy.PNG){#Fig:CreateCourse
width=".95\\textwidth"}

Test Objective: Given a directory, does the system read in and display all images in the hierarchy in a top-down traversal?
---------------------------------------------------------------------------------------------------------------------------

Test ran

    python image_browser.py C:\Users\sclar\TestDirectory

Test result: Image browser popped up with butterfly.png and traversed
into directories and sub-directory in top-down order

Test Objective: Given a directory, does the system preserve the aspect ration of the users OS and ensure that the image fits inside the window. (Platforms checked: Windows and MacOS X)
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Test ran

    python image_browser.py C:\Users\sclar\TestDirectory

Test result: On both the Windows 10 and Mac OS used for testing, the
images fit inside the window of the image browser and the aspect ration
was preserved. (after finding that it did not and changes were made to
the code :))

Test Objective: Is the metadata for each image displayed in the browser including name and size?
------------------------------------------------------------------------------------------------

Test ran

    python image_browser.py C:\Users\sclar\TestDirectory

Test result: Metadata is displayed on the split pane of the browser,
including file path. A button is included that returns the content
relevant to the operating system and the file.

Test Objective: Determine what happens at the end case where a file is given as dir that is not an image.
---------------------------------------------------------------------------------------------------------

Test ran

    python image_browser.py C:\Users\sclar\TestDirectory\requirements.txt

Test result:

    Invalid path or there are no images in path

Test Objective: Determine what happens if user does not enter in required parameter dir
---------------------------------------------------------------------------------------

Test ran

    python image_browser.py

Test result:

    usage: image_browser.py [-h] [--rows ROWS] [--cols COLS] dir
    image_browser.py: error: the following arguments are required: dir

Testing Objective: What is the result of using the optional -h flag?
--------------------------------------------------------------------

Test ran

    C:\Users\sclar\Documents\Git\image-browser>python image_browser.py -h

Test result:

    usage: image_browser.py [-h] [--rows ROWS] [--cols COLS] dir

    Image browser v1.0

    positional arguments:
      dir          The root directory to view photos in

    optional arguments:
      -h, --help   show this help message and exit
      --rows ROWS  Max number of rows on screen (Default is 720)
      --cols COLS  Max number of columns on screen (Default is 1080)

Testing Objective: Is the user able to traverse the images using 'n' for next, 'p' for previous including handling going back to the beginning of the slides when at the end and to the beginning of the slide show when at the end. In addition can the user quit with q?
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Test ran

    python image_browser.py C:\Users\sclar\TestDirectory

Test results: Successful traversal from beginning to end using 'n',
going backwards with 'p', moving from end to beginning, moving from
beginning to end. The application terminates with 'q.'

Testing Objective: Did the team use OpenCv techniques and Affine transformations in their implementation?
---------------------------------------------------------------------------------------------------------

Test ran

    python image_browser.py C:\Users\sclar\TestDirectory

Test results: Affine functionality is included as a button on the
browser window. When user selects the button AffineT, the image is
transformed to a new image that is \"sheared\" so that the pixels
neighbors are preserved with but the locations are all shifted relative
to a new position.

Testing Objective: Can the user enter in a specified max number of columns and rows with the optional flags?
------------------------------------------------------------------------------------------------------------

Test ran

    python image_browser.py --cols 90 --rows 90 C:\Users\sclar\TestDirectory

Test result: Using such a small maximum row and col size (both equal),
it was noted that the image was always square and very small\...but the
entire image stayed in the browser.

Reflecting on the learning experience and teamwork
==================================================

Reflect on your solution to the problem and the learning experience
through this project. Trust building, cohesion, and psychological safety
are the foundations elements of teamwork. Reflect on the team dynamic
experienced in this project.

Team member contribution/effort assessment
------------------------------------------

The following rubric is used by the members of the team in order to rate
themselves and their teams members on a scale of 1 to 5 about their
individual contribution to the project (a rating of 1 being poor and 5
being outstanding). Rationale should be provided for each rating. These
documents are seperate.

::: {#tab:table1}
| &nbsp;            | Self-assessment | Team member 1 | Team member 2 |
| ----------------- | --------------- | ------------- | ------------- |
| attended meetings |                 |               |               |
| communicated      |                 |               |               |
| participated      |                 |               |               |
| contributed       |                 |               |               |
| provided feedback |                 |               |               |
| positive attitude |                 |               |               |

  : Team Assessment.
:::

The rubric for scoring is given in the following image:

![\"Team member assessment
rubric\"](images/rheubric.PNG){#Fig:CreateCourse width=".95\\textwidth"}
