package com.emlakcepte.model;

public class Search
{
	private String province;
	private String district;
	
	
	public String getProvince()
	{
		return province;
	}
	public void setProvince(String province)
	{
		this.province = province;
	}
	public String getDistrict()
	{
		return district;
	}
	public void setDistrict(String district)
	{
		this.district = district;
	}
	
	@Override
	public String toString()
	{
		return "Search [province=" + province + ", district=" + district + "]";
	}
	
	

}
