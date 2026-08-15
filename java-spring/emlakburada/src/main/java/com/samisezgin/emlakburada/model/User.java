package com.samisezgin.emlakburada.model;

import java.time.LocalDateTime;
import java.util.List;

import javax.persistence.*;

import com.samisezgin.emlakburada.model.enums.UserType;

@Entity
@Table(name = "users")
public class User
{
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "id")
	private long id;

	@Column(name = "firstName")
	private String firstName;

	@Column(name = "lastName")
	private String lastName;

	@Column(name = "email")
	private String email;

	@Column(name = "password")
	private String password;

	@Column(name = "userType")
	private UserType userType;

	@OneToMany(fetch = FetchType.LAZY, cascade = CascadeType.ALL)
	private List<RealEstate> realEstates;
	
	@OneToMany(fetch = FetchType.LAZY, cascade = CascadeType.ALL)
	private List<RealEstate> favoriteRealEstates;
	
	@OneToMany(fetch = FetchType.LAZY, cascade = CascadeType.ALL)
	private List<Message> messages;

	private LocalDateTime createDate;

	public User()
	{
		super();
	}

	public User(String firstName, String lastName, String email, String password, UserType userType)
	{
		super();
		this.firstName = firstName;
		this.lastName = lastName;
		this.email = email;
		this.password = password;
		this.userType = userType;
		this.createDate = LocalDateTime.now();
	}

	public User(String firstName, String lastName)
	{
		super();
		this.firstName = firstName;
		this.lastName = lastName;
	}

	public String getFirstName()
	{
		return firstName;
	}

	public void setFirstName(String firstName)
	{
		this.firstName = firstName;
	}

	public String getLastName()
	{
		return lastName;
	}

	public void setLastName(String lastName)
	{
		this.lastName = lastName;
	}

	public long getId()
	{
		return id;
	}

	@Override
	public String toString()
	{
		return "User [firstName=" + firstName + ", lastName=" + lastName + "]";
	}

	public List<RealEstate> getRealEstates()
	{
		return realEstates;
	}

	public void setRealEstates(List<RealEstate> realEstates)
	{
		this.realEstates = realEstates;
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

	public UserType getUserType()
	{
		return userType;
	}

	public void setUserType(UserType userType)
	{
		this.userType = userType;
	}

	public List<RealEstate> getFavoriteRealEstates()
	{
		return favoriteRealEstates;
	}

	public void setFavoriteRealEstates(List<RealEstate> favoriteRealEstates)
	{
		this.favoriteRealEstates = favoriteRealEstates;
	}

	public List<Message> getMessages()
	{
		return messages;
	}

	public void setMessages(List<Message> messages)
	{
		this.messages = messages;
	}

	public LocalDateTime getCreateDate()
	{
		return createDate;
	}

	public void setCreateDate(LocalDateTime createDate)
	{
		this.createDate = createDate;
	}

}
