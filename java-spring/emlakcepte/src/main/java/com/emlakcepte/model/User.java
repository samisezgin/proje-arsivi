package com.emlakcepte.model;

import java.time.LocalDateTime;
import java.util.List;

public class User
{
	private String name;
	private String email;
	private String password;
	private UserType userType;
	private List<Realty> realtyList;
	private List<Realty> favoriteRealtyList;
	private List<Message> messages;
	private LocalDateTime createDate;
	private List<Search> searches;

	public User()
	{
		super();
	}
	
	
	
	

	public User(String name, String email, String password)
	{
		super();
		this.name = name;
		this.email = email;
		this.password = password;
	}





	public List<Realty> getFavoriteRealtyList()
	{
		return favoriteRealtyList;
	}

	public void setFavoriteRealtyList(List<Realty> favoriteRealtyList)
	{
		this.favoriteRealtyList = favoriteRealtyList;
	}

	public List<Message> getMessages()
	{
		return messages;
	}

	public void setMessages(List<Message> messages)
	{
		this.messages = messages;
	}

	public User(String name, String email, String password, List<Realty> realtyList)
	{
		this.name = name;
		this.email = email;
		this.password = password;
		this.realtyList = realtyList;
		this.setCreateDate(LocalDateTime.now());
	}

	public String getName()
	{
		return name;
	}

	public void setName(String name)
	{
		this.name = name;
	}

	public String getEmail()
	{
		return email;
	}

	public void setEmail(String email)
	{
		this.email = email;
	}

	public String getPassword()
	{
		return password;
	}

	public void setPassword(String password)
	{
		this.password = password;
	}

	public List<Realty> getRealtyList()
	{
		return realtyList;
	}

	public void setRealtyList(List<Realty> realtyList)
	{
		this.realtyList = realtyList;
	}

	public LocalDateTime getCreateDate()
	{
		return createDate;
	}

	public void setCreateDate(LocalDateTime createDate)
	{
		this.createDate = createDate;
	}

	@Override
	public String toString()
	{
		return "User [name=" + name + "]";
	}

	public UserType getUserType()
	{
		return userType;
	}

	public void setUserType(UserType userType)
	{
		this.userType = userType;
	}

	public List<Search> getSearches()
	{
		return searches;
	}

	public void setSearches(List<Search> searches)
	{
		this.searches = searches;
	}

}
