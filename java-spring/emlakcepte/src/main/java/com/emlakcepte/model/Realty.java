package com.emlakcepte.model;

import java.time.LocalDate;

public class Realty
{

	private long realtyNo;
	private String title;
	private LocalDate publishDate;
	private User user;
	private RealtyPublishStatus status;	
	private String province;
	private String district;
	private RealtyType realtyType; 
	private RealtyCategory category;

	public Realty()
	{
		super();
		this.publishDate = LocalDate.now();
	}
	
	

	public Realty(long realtyNo, String title, LocalDate publishDate, User user, RealtyPublishStatus status)
	{
		super();
		this.realtyNo = realtyNo;
		this.title = title;
		this.publishDate = publishDate;
		this.user = user;
		this.status = status;
	}



	public long getRealtyNo()
	{
		return realtyNo;
	}

	public void setRealtyNo(long realtyNo)
	{
		this.realtyNo = realtyNo;
	}

	public String getTitle()
	{
		return title;
	}

	public void setTitle(String title)
	{
		this.title = title;
	}

	public LocalDate getPublishDate()
	{
		return publishDate;
	}

	public void setPublishDate(LocalDate publishDate)
	{
		this.publishDate = publishDate;
	}

	public User getUser()
	{
		return user;
	}

	public void setUser(User user)
	{
		this.user = user;
	}

	public RealtyPublishStatus getStatus()
	{
		return status;
	}

	public void setStatus(RealtyPublishStatus status)
	{
		this.status = status;
	}

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

	public RealtyType getRealtyType()
	{
		return realtyType;
	}

	public void setRealtyType(RealtyType realtyType)
	{
		this.realtyType = realtyType;
	}

	public RealtyCategory getCategory()
	{
		return category;
	}

	public void setCategory(RealtyCategory category)
	{
		this.category = category;
	}

	@Override
	public String toString()
	{
		return "Realty [realtyNo=" + realtyNo + ", title=" + title + ", publishDate=" + publishDate + ", user=" + user
				+ ", status=" + status + ", province=" + province + ", district=" + district + ", realtyType="
				+ realtyType + ", category=" + category + "]";
	}

	

}
