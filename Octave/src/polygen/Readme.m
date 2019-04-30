% Copyright (C) 2010-13 - Pieter V. Reyneke, South Africa
%
% Open Source licence, use whereever you like but at own risk, keep this
% complete copyright notice in the codeset and please send me updates and 
% report errors to pieter.reyneke@gmail.com. Will give recognition, if
% requested, after any valid comment leading to an update was recieved. 
%
% Author: PV Reyneke
% Email : pieter.reyneke@gmail.com
%
% The main functions are
% 1. legendre_gamma_test.m     - Checks the EMP polinomial coefficients against
%    gamma_EMP_coefficients.m    previously published ones, if you would like
%    (extended to 8th degree)    to extend above 4th degree, copy the contained
%                                function gamma_EMP_polynomial to its owns 
%                                file and run in a similar loop without comparing.
% 2. laguerre_gamma_test.m     - Checks the FMP polinomial coefficients against
%    gamma_FMP_coefficients.m    previously published ones, if you would like
%    (extended to 8th degree)    to extend above 4th degree, copy the contained
%                                function gamma_FMP_polynomial to its owns 
%                                file and run in a similar loop without comparing.
% 3. vrf_diag_emp.m            - Displaying the VRF diagonals only.
% 4. vrf_diag_fmp.m            - Displaying the VRF diagonals only.
% 5. Ns_E2F.m                  - Displays the switching point approximations.
% 6. vrf_all.m                 - This function is an example if one would
%                                like to calculate the off-diagonal VRF terms.
% 7. Polynomial_Coeffs_VRFs_and_Ns_08.pdf
%                              - A document with generated diagonals and
%                                coefficients up to the 8th degree.
