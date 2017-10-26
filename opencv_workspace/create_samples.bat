rmdir /s /q refined
mkdir refined

cd refined

mkdir clouds
mkdir waterspout
mkdir negs

cd ..

python refine.py

pause

cd refined

copy /y NUL clouds_vector.vec
copy /y NUL waterspout_vector.vec

C:\Users\gaged\OpenCV\opencv\build\x64\vc14\bin\opencv_createsamples.exe ^
-info clouds_info.data -vec clouds_vector.vec -bg neg_info.data -w 40 -h 40

C:\Users\gaged\OpenCV\opencv\build\x64\vc14\bin\opencv_createsamples.exe ^
-info waterspout_info.data -vec waterspout_vector.vec -bg neg_info.data -w 40 -h 40

pause
