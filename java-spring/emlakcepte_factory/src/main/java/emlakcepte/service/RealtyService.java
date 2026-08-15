package emlakcepte.service;

import java.util.List;

import emlakcepte.dao.RealtyDao;
import emlakcepte.model.Realty;
import emlakcepte.model.RealtyCategory;
import emlakcepte.model.RealtyPublishStatus;
import emlakcepte.model.RealtyType;
import emlakcepte.model.User;
import interfaces.IRealtyService;

public class RealtyService implements IRealtyService
{

	private RealtyDao realtyDao = new RealtyDao();

	public void createRealty(Realty realty)
	{

		realtyDao.createRealty(realty);
		System.out.println("İlan: " + realty.getTitle() + " eklendi.");

		/*
		 * boolean cond1=realty.getUser().getUserType().equals(UserType.INDIVIDUAL);
		 * boolean cond2=realty.getUser().getRealtyList().size()<3;
		 * 
		 * if(!(cond1&&cond2)) {
		 * System.out.println("Bireysel müşteri 3'ten fazla ilan paylaşamaz."); return;
		 * }
		 * 
		 * realtyDao.createRealty(realty);
		 * System.out.println("İlan: "+realty.getTitle()+" eklendi.");
		 */

	}

	public List<Realty> getAll()
	{
		return realtyDao.getAll();
	}

	public void printAll()
	{
		getAll().forEach(realty -> System.out.println(realty));
	}

	public void printByProvince(String province)
	{
		getAll().stream().filter(realty -> realty.getProvince().equals(province))
				.forEach(realty -> System.out.println(realty));
	}

	public void getAllByProvinceAndDistrict(String province, String district)
	{
		getAll().stream().filter(realty -> realty.getProvince().equals(province))
				.filter(realty -> realty.getDistrict().equals(district)).forEach(System.out::println);
	}

	public long getRealtyNumberInProvince(String province)
	{
		return getAll().stream().filter(realty -> realty.getProvince().equals(province)).count();
	}

	public long getRealtyNumberInProvince(List<String> provinces)
	{
		return getAll().stream().filter(realty -> provinces.contains(realty.getProvince())).count();
	}

	public long getHouseNumberInProvince(String province, RealtyCategory category)
	{
		return getAll().stream().filter(realty -> realty.getProvince().equals(province))
				.filter(realty -> realty.getRealtyType().equals(RealtyType.HOUSE))
				.filter(realty -> realty.getCategory().equals(category)).count();
	}

	public void showCaseByProvince(String province)
	{
		getAll().stream().filter(realty -> realty.getProvince().equals(province)).limit(10)
				.forEach(System.out::println);
	}

	public List<Realty> getAllByUsername(User user)
	{
		return getAll().stream().filter(realty -> realty.getUser().getName().equals(user.getName())).toList();
	}

	public void printAllByUsername(User user)
	{
		getAll().stream().filter(realty -> realty.getUser().getName().equals(user.getName())).toList()
				.forEach(realty -> System.out.println(realty));
	}

	public List<Realty> getAllByActive()
	{
		return getAll().stream().filter(realty -> realty.getStatus().equals(RealtyPublishStatus.ACTIVE)).toList();
	}

	public void printAllByActive()
	{
		getAllByActive().forEach(realty -> System.out.println(realty));
	}

}
