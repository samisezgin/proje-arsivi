package com.clonemedium.services;

import java.util.List;
import java.util.Scanner;

import org.springframework.stereotype.Service;

import com.clonemedium.model.Blog;
import com.clonemedium.model.Tag;
import com.clonemedium.model.User;
import com.clonemedium.repository.UserRepository;

@Service
public class UserService
{
	private UserRepository userDao = new UserRepository();

	private static Scanner scanner = new Scanner(System.in);

	public User createUser(User user)
	{
		if (user.getPassword().trim().isEmpty() || user.getPassword().length() < 5)
		{
			System.out.println("The password must be longer than 5 characters!");
			return null;
		}
		userDao.createUser(user);
		return user;
	}

	public List<User> getAll()
	{
		return userDao.getAll();
	}

	

	public void printBlogByUser(User user)
	{
		userDao.getAll().stream().filter(usr -> usr.getUserName().equalsIgnoreCase(user.getUserName()))
				.forEach(usr1 -> usr1.getBlogs().forEach(blog -> System.out.println("Blog Title: "+blog.getTitle()+"\tBlog status: "+blog.getBlogStatus())));
	}
	
	public void printBlogByUser(String userName)
	{
		userDao.getAll().stream().filter(usr -> usr.getUserName().equalsIgnoreCase(userName))
				.forEach(usr1 -> usr1.getBlogs().forEach(blog -> System.out.println("Blog Title: "+blog.getTitle()+"\tBlog status: "+blog.getBlogStatus())));
	}

	public void writeDraft(User user, Blog blog)
	{
		String ans;
		do
		{
			System.out.println("Do you want to publish the blog?(Y/N)");
			ans = scanner.nextLine();
			if (!(ans.equalsIgnoreCase("y") || ans.equalsIgnoreCase("n")))
			{
				System.out.println("Wrong choice, try again.");
				continue;
			}
			userDao.writeDraft(user, blog, ans);
		} while (ans.equalsIgnoreCase("y") || ans.equalsIgnoreCase("n"));

	}

	public void deleteBlog(User user, Blog blog)
	{
		userDao.deleteBlog(user, blog);
	}

	public void followUser(User src, User dst)
	{
		userDao.followUser(src, dst);
	}

	public void unFollowUser(User src, User dst)
	{
		userDao.unFollowUser(src, dst);
	}

	public void followTag(User user, Tag tag)
	{
		userDao.followTag(user, tag);
	}

	public void unFollowTag(User user, Tag tag)
	{
		userDao.unFollowTag(user, tag);
	}

	public void printFollowedUsers(User user)
	{
		user.getFollowedUsers().forEach(user1 -> System.out.println(user1.getUserName()));

	}

}
