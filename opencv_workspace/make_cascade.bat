cd clouds

REM cd cirrus
REM rmdir /s /q cascade
REM mkdir cascade
REM C:\Users\gaged\OpenCV\opencv\build\x64\vc14\bin\opencv_traincascade.exe ^
REM -data cascade -vec vector.ai -bg ../../negs/info.data ^
REM -numPos 69 -numNeg 97

REM pause

cd cumulus
rmdir /s /q cascade
mkdir cascade
C:\Users\gaged\OpenCV\opencv\build\x64\vc14\bin\opencv_traincascade.exe ^
-data cascade -vec vector.ai -bg ../../negs/info.data ^
-numPos 40 -numNeg 94 -numStages 10

pause

REM cd stratus
REM rmdir /s /q cascade
REM mkdir cascade
REM C:\Users\gaged\OpenCV\opencv\build\x64\vc14\bin\opencv_traincascade.exe ^
REM -data cascade -vec vector.ai -bg ../../negs/info.data ^
REM -numPos 229 -numNeg 97

REM pause
