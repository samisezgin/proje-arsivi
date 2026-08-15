
import emlakcepte.service.RealtyService;
import emlakcepte.service.UserService;

public class Main
{
	public static void main(String[] args)
	{

		UserService userService1 = UserService.getInstance();
		UserService userService2 = UserService.getInstance();
		RealtyService realtyService1 = RealtyService.getInstance();
		RealtyService realtyService2 = RealtyService.getInstance();

		System.out.println(userService1==userService2);
		System.out.println(realtyService1==realtyService2);

	}

	

}
