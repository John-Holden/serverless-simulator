test:
	 cd tree_epi_back/src && pytest

 compile_SIR:
	 cd tree_epi_back/cpp_executable && \
 	 g++ -c -fPIC generic_SIR.cpp -o generic_SIR.o && \
 	 g++ -shared -Wl,-soname,libSIR.so -o libSIR.so  generic_SIR.o
