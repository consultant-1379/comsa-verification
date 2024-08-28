/*
*  For Unit Test for getRoles of Access Management
*/
#include <stdio.h>
#include <stdlib.h>
//#include <ComSA.h>
#include "RoleClientHandler.h"


int main(int argc, char **argv)
{
	char **roles = NULL;
	char* user = getlogin();
	if (argc > 1)
		user = argv[1];

	printf("Getting roles for user: %s\n", user);

	GetRolesReturnT result = getRoles(user, "Roles", &roles);

	char rs[512] = { 0 };
	int i = 0;
	if (roles != NULL)
	{
		for (i=0; roles[i] != NULL; i++)
		{
			if (i != 0)
			{
				strcat( rs, ", ");
			}
			sprintf(rs, "%s%s", rs, roles[i]);
		}
	}

	printf("%s has role(s):%s\n", user, rs);

	freeRoles(roles);

	return result;

}



