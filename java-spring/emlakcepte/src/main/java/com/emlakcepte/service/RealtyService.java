package com.emlakcepte.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.emlakcepte.model.Realty;
import com.emlakcepte.model.RealtyCategory;
import com.emlakcepte.model.RealtyPublishStatus;
import com.emlakcepte.model.RealtyType;
import com.emlakcepte.model.User;
import com.emlakcepte.model.UserType;
import com.emlakcepte.repository.RealtyRepository;

//@Service
public class RealtyService
{
	private RealtyRepository realtyRepository;

	public void createRealty(Realty realty)
	{
		
		if (realty.getUser().getUserType().equals(UserType.INDIVIDUAL) && realty.getRealtyType().equals(RealtyType.HOUSE))
		{
			if(realty.getUser().getRealtyList().size()<3)
			{
				realtyRepository.createRealty(realty);
				System.out.println("İlan: "+realty.getTitle()+" eklendi.");
			}
			else
			{
				System.out.println("Bireysel müşteri 3'ten fazla ilan paylaşamaz.");
			}
		}
		else
		{
			realtyRepository.createRealty(realty);
			System.out.println("İlan: "+realty.getTitle()+" eklendi.");
		}
		
		/*boolean cond1=realty.getUser().getUserType().equals(UserType.INDIVIDUAL);
		boolean cond2=realty.getUser().getRealtyList().size()<3;
		
		if(!(cond1&&cond2))
		{
			System.out.println("Bireysel müşteri 3'ten fazla ilan paylaşamaz.");
			return;
		}
		
		realtyDao.createRealty(realty);
		System.out.println("İlan: "+realty.getTitle()+" eklendi.");*/
		
	}

	public List<Realty> getAll()
	{
		return realtyRepository.getAll();
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
	
	/*public void getAllByProvinceAndDistrict(String province, String district)
	{
		getAll().stream().filter(realty->realty.getProvince().equals(province))
		.filter(realty->realty.getDistrict().equals(district)).forEach(System.out::println);
	}*/
	
	public List<Realty> getAllByProvinceAndDistrict(String province, String district)
	{
		return getAll().stream().filter(realty->realty.getProvince().equals(province))
		.filter(realty->realty.getDistrict().equals(district)).toList();
	}
	
	public long getRealtyNumberInProvince(String province)
	{
		return getAll().stream().filter(realty->realty.getProvince().equals(province)).count();
	}
	
	public long getRealtyNumberInProvince(List<String> provinces)
	{
		return getAll().stream().filter(realty -> provinces.contains(realty.getProvince())).count();
	}
	
	public long getHouseNumberInProvince(String province, RealtyCategory category)
	{
		return getAll().stream()
				.filter(realty->realty.getProvince().equals(province))
				.filter(realty->realty.getRealtyType().equals(RealtyType.HOUSE))
				.filter(realty->realty.getCategory().equals(category)).count();
	}
	
	/*public void showCaseByProvince(String province)
	{
		getAll().stream()
		.filter(realty -> realty.getProvince().equals(province))
		.limit(10).forEach(System.out::println);
	}*/
	

	public List<Realty> showCaseByProvince(String province)
	{
		getAll().stream()
		.filter(realty -> realty.getProvince().equals(province))
		.limit(10).forEach(System.out::println);
		return getAll().stream()
		.filter(realty -> realty.getProvince().equals(province))
		.limit(10).toList();
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
