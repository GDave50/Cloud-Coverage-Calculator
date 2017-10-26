cd refined

rmdir /s /q clouds_cascade
mkdir clouds_cascade

C:\Users\gaged\OpenCV\opencv\build\x64\vc14\bin\opencv_traincascade.exe ^
-data clouds_cascade -vec clouds_vector.vec -bg neg_info.data ^
-numPos 300 -numNeg 511 -w 40 -h 40

pause

mkdir ..\cascades

copy /y clouds_cascade\cascade.xml ..\cascades\cloudsCascade.xml

rmdir /s /q waterspout_cascade
mkdir waterspout_cascade

C:\Users\gaged\OpenCV\opencv\build\x64\vc14\bin\opencv_traincascade.exe ^
-data waterspout_cascade -vec waterspout_vector.vec -bg neg_info.data ^
-numPos 29 -numNeg 511 -w 40 -h 40

pause

copy /y waterspout_cascade\cascade.xml ..\cascades\waterspoutCascade.xml
