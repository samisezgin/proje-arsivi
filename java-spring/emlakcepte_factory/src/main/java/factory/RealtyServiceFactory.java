package factory;

import emlakcepte.service.RealtyService;
import interfaces.IRealtyService;

public class RealtyServiceFactory
{
	public IRealtyService getRealtyService(String type)
	{
		if(type.equalsIgnoreCase("realtyservice"))
		{
			return new RealtyService();
		}		
		return null;
	}
}
