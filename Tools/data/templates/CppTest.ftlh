/***** ${scope}
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ TEST
 */

#include <iostream>
#include <vector>
#include <cmath>
#include <netcdf.h>

#include <doctest.h>

${systemIncludes}
${interfaceInclude}
${localIncludes}



#pragma float_control(push)
#pragma float_control(precise, off)
${cppBody}
#pragma float_control(pop)

${doctest}
