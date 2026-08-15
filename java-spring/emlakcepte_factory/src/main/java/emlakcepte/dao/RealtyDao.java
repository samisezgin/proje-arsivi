package emlakcepte.dao;

import java.util.ArrayList;
import java.util.List;

import emlakcepte.model.Realty;

public class RealtyDao
{
	private static List<Realty> realtyList = new ArrayList<>();
	
	public void createRealty(Realty realty)
	{
		realtyList.add(realty);
		System.out.println("createRealty :: "+realty.getTitle());
	}

	public List<Realty> getAll()
	{
		return realtyList;
	}

}
