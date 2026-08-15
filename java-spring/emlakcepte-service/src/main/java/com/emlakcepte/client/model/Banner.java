package com.emlakcepte.client.model;

public class Banner
{
	private int adet;
	private String ilanNo;
	private String telNo1;
	private String telNo2;
	
	public Banner() {}
	public Banner(int adet, String ilanNo, String telNo1, String telNo2)
	{
		super();
		this.adet = adet;
		this.ilanNo = ilanNo;
		this.telNo1 = telNo1;
		this.telNo2 = telNo2;
	}

	public int getAdet()
	{
		return adet;
	}

	public void setAdet(int adet)
	{
		this.adet = adet;
	}

	public String getIlanNo()
	{
		return ilanNo;
	}

	public void setIlanNo(String ilanNo)
	{
		this.ilanNo = ilanNo;
	}

	public String getTelNo1()
	{
		return telNo1;
	}

	public void setTelNo1(String telNo1)
	{
		this.telNo1 = telNo1;
	}

	public String getTelNo2()
	{
		return telNo2;
	}

	public void setTelNo2(String telNo2)
	{
		this.telNo2 = telNo2;
	}

	@Override
	public String toString()
	{
		return "Banner [adet=" + adet + ", ilanNo=" + ilanNo + ", telNo1=" + telNo1 + ", telNo2=" + telNo2 + "]";
	}

}
