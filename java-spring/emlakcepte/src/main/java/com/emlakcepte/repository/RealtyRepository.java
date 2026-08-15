package com.emlakcepte.repository;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Component;

import com.emlakcepte.model.Realty;

@Component
public class RealtyRepository
{
	private static List<Realty> realtyList = new ArrayList<>();
	
	public void createRealty(Realty realty)
	{
		realtyList.add(realty);
		realty.getUser().getRealtyList().add(realty);
		System.out.println("createRealty :: "+realty.getTitle());
	}

	public List<Realty> getAll()
	{
		return realtyList;
	}

}
