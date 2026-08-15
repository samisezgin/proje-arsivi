import emlakcepte.model.Realty;
import emlakcepte.model.User;
import factory.RealtyServiceFactory;
import factory.UserServiceFactory;
import interfaces.IRealtyService;
import interfaces.IUserService;

public class Main
{
	public static void main(String[] args)
	{

		RealtyServiceFactory realtyServiceFactory = new RealtyServiceFactory();
		IRealtyService realtyService=realtyServiceFactory.getRealtyService("REALTYSERVICE");
	
		UserServiceFactory userServiceFactory = new UserServiceFactory();
		IUserService userService=userServiceFactory.getUserService("USERSERVICE");
		
		Realty realty1=new Realty();
		User user1=new User();
		
		realtyService.createRealty(realty1);
		userService.createUser(user1);
		
		userService.getAllUsers();
		realtyService.getAll();
		
	}

	
}
