//testMain.cpp

#define DOCTEST_CONFIG_IMPLEMENT
#include <doctest.h>


int main(int argc, char** argv) {
	doctest::Context  context;
	char* args[] = { "", "-d", NULL };
	context.applyCommandLine(2, args);
	int i = context.run(); // output);
	return i;
}