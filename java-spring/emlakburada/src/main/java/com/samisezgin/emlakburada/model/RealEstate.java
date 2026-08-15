package com.samisezgin.emlakburada.model;

import javax.persistence.*;


@Entity
@Table(name = "realestate")
public class RealEstate
{
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;
	@Column(name = "title", nullable = false, length = 100)
	private String title;
	@ManyToOne
	@JoinColumn(name="user_id", referencedColumnName="id",nullable=false)
	private User user;
	public RealEstate()
	{
		super();
	}
	
	public RealEstate(String title, User user)
	{
		super();
		this.title = title;
		this.user = user;
	}

	public String getTitle()
	{
		return title;
	}

	public void setTitle(String title)
	{
		this.title = title;
	}

	public User getUser()
	{
		return user;
	}

	public void setUser(User user)
	{
		this.user = user;
	}

	public Integer getId()
	{
		return id;
	}
	
	
	
}
