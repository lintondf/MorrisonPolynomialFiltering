//testMain.cpp

#define DOCTEST_CONFIG_IMPLEMENT
#include <doctest.h>


int main(int argc, char** argv) {
	doctest::Context  context;
	context.applyCommandLine(argc, argv);
	int i = context.run(); // output);
	return i;
}