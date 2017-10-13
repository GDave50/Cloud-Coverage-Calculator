:: run the python program that makes all info.data files
python main.py

:: wait
pause

cd ../clouds

:: goto cirrus folder
cd cirrus

:: replace/make vector file
copy /y NUL vector.ai

:: run opencv_creatsamples.exe
C:\Users\gaged\OpenCV\opencv\build\x64\vc14\bin\opencv_createsamples.exe ^
-info info.data -vec vector.ai -bg ../../negs/info.data

:: wait
pause

:: goto cumulus folder
cd ../cumulus

:: replace/make vector file
copy /y NUL vector.ai

:: run opencv_creatsamples.exe
C:\Users\gaged\OpenCV\opencv\build\x64\vc14\bin\opencv_createsamples.exe ^
-info info.data -vec vector.ai -bg ../../negs/info.data

:: wait
pause

:: goto stratus folder
cd ../stratus

:: replace/make vector file
copy /y NUL vector.ai

:: run opencv_creatsamples.exe
C:\Users\gaged\OpenCV\opencv\build\x64\vc14\bin\opencv_createsamples.exe ^
-info info.data -vec vector.ai -bg ../../negs/info.data

:: wait
pause

:: goto waterspout folder
cd ../waterspout

:: replace/make vector file
copy /y NUL vector.ai

:: run opencv_creatsamples.exe
C:\Users\gaged\OpenCV\opencv\build\x64\vc14\bin\opencv_createsamples.exe ^
-info info.data -vec vector.ai -bg ../../negs/info.data

:: wait
pause
