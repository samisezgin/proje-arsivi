package factory;

import emlakcepte.service.UserService;
import interfaces.IUserService;

public class UserServiceFactory
{
	public IUserService getUserService(String type)
	{
		if(type.equalsIgnoreCase("userservice"))
		{
			return new UserService();
		}		
		return null;
	}
}
