/* This file generated automatically. */ 
/* Do not modify. */ 
#include "udf.h" 
#include "prop.h" 
#include "dpm.h" 
extern DEFINE_ON_DEMAND(Print_input_file);
extern DEFINE_ON_DEMAND(load_input_data);
extern DEFINE_ON_DEMAND(Write_xyz_file); 
extern DEFINE_ON_DEMAND(Rename_UDMs);
extern DEFINE_EXECUTE_AT_END(Calculate_Joule_Heating);
extern DEFINE_EXECUTE_AT_END(Calculate_Lorentz_Force);
extern DEFINE_EXECUTE_AT_END(Assign_Temperature);
extern DEFINE_ON_DEMAND(Assign_Temperature_Demand);
extern DEFINE_DIFFUSIVITY(conductivity_varying_wrt_temperature, c, tc, i);
extern DEFINE_DIFFUSIVITY(conductivity_patch_on_marked_region, c, tc, i);
extern DEFINE_EXECUTE_AT_END(FluentCallMaxwell_Cplg);
extern DEFINE_SOURCE(joule_heating,c,t,dS,eqn);
extern DEFINE_SOURCE(Lorentz_X_momentum,c,t,dS,eqn);
extern DEFINE_SOURCE(Lorentz_Y_momentum,c,t,dS,eqn);
extern DEFINE_SOURCE(Lorentz_Z_momentum,c,t,dS,eqn);
extern DEFINE_ON_DEMAND(Test_mapp_sigma);
extern DEFINE_ON_DEMAND(Test_call_maxwell); 
extern DEFINE_ON_DEMAND(Test_Write_Field_into_UDM);
__declspec(dllexport) UDF_Data udf_data[] = { 
{"Print_input_file", (void (*)(void))Print_input_file, UDF_TYPE_ON_DEMAND},
{"load_input_data", (void (*)(void))load_input_data, UDF_TYPE_ON_DEMAND},
{"Write_xyz_file", (void (*)(void))Write_xyz_file, UDF_TYPE_ON_DEMAND}, 
{"Rename_UDMs", (void (*)(void))Rename_UDMs, UDF_TYPE_ON_DEMAND},
{"Calculate_Joule_Heating", (void (*)(void))Calculate_Joule_Heating, UDF_TYPE_EXECUTE_AT_END},
{"Calculate_Lorentz_Force", (void (*)(void))Calculate_Lorentz_Force, UDF_TYPE_EXECUTE_AT_END},
{"Assign_Temperature", (void (*)(void))Assign_Temperature, UDF_TYPE_EXECUTE_AT_END},
{"Assign_Temperature_Demand", (void (*)(void))Assign_Temperature_Demand, UDF_TYPE_ON_DEMAND},
{"conductivity_varying_wrt_temperature", (void (*)(void))conductivity_varying_wrt_temperature, UDF_TYPE_DIFFUSIVITY},
{"conductivity_patch_on_marked_region", (void (*)(void))conductivity_patch_on_marked_region, UDF_TYPE_DIFFUSIVITY},
{"FluentCallMaxwell_Cplg", (void (*)(void))FluentCallMaxwell_Cplg, UDF_TYPE_EXECUTE_AT_END},
{"joule_heating", (void (*)(void))joule_heating, UDF_TYPE_SOURCE},
{"Lorentz_X_momentum", (void (*)(void))Lorentz_X_momentum, UDF_TYPE_SOURCE},
{"Lorentz_Y_momentum", (void (*)(void))Lorentz_Y_momentum, UDF_TYPE_SOURCE},
{"Lorentz_Z_momentum", (void (*)(void))Lorentz_Z_momentum, UDF_TYPE_SOURCE},
{"Test_mapp_sigma", (void (*)(void))Test_mapp_sigma, UDF_TYPE_ON_DEMAND},
{"Test_call_maxwell", (void (*)(void))Test_call_maxwell, UDF_TYPE_ON_DEMAND}, 
{"Test_Write_Field_into_UDM", (void (*)(void))Test_Write_Field_into_UDM, UDF_TYPE_ON_DEMAND},
}; 
__declspec(dllexport) int n_udf_data = sizeof(udf_data)/sizeof(UDF_Data); 
#include "version.h" 
__declspec(dllexport) void UDF_Inquire_Release(int *major, int *minor, int *revision) 
{ 
*major = RampantReleaseMajor; 
*minor = RampantReleaseMinor; 
*revision = RampantReleaseRevision; 
} 
