package com.clonemedium.repository;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Repository;

import com.clonemedium.model.Blog;
import com.clonemedium.model.BlogStatus;
import com.clonemedium.model.Tag;
import com.clonemedium.model.User;

@Repository
public class UserRepository
{
	private static List<User> userList = new ArrayList<User>();

	private TagRepository tagRepository = new TagRepository();

	private BlogRepository blogRepository = new BlogRepository();

	public User createUser(User user)
	{
		userList.add(user);
		return user;
	}

	public List<User> getAll()
	{
		return userList;
	}

	public void followUser(User src, User dst)
	{
		if (!userList.contains(src))
		{
			System.out.println("Source user not found!");
			return;
		}
		if (!userList.contains(dst))
		{
			System.out.println("Destination user not found!");
			return;
		}
		src.getFollowedUsers().add(dst);
		dst.getFollowerUsers().add(src);
	}

	public void unFollowUser(User src, User dst)
	{
		if (!userList.contains(src))
		{
			System.out.println("Source user not found!");
			return;
		}
		if (!userList.contains(dst))
		{
			System.out.println("Destination user not found!");
			return;
		}
		src.getFollowedUsers().remove(dst);
		dst.getFollowerUsers().remove(src);
	}

	public void followTag(User user, Tag tag)
	{
		if (!userList.contains(user))
		{
			System.out.println("User not found!");
			return;
		}
		if (!tagRepository.getAll().contains(tag))
		{
			System.out.println("Tag not found!");
			return;
		}
		user.getFollowedTags().add(tag);

	}

	public void unFollowTag(User user, Tag tag)
	{
		if (!userList.contains(user))
		{
			System.out.println("User not found!");
			return;
		}
		if (!tagRepository.getAll().contains(tag))
		{
			System.out.println("Tag not found!");
			return;
		}
		user.getFollowedTags().remove(tag);
	}

	public void writeDraft(User user, Blog blog, String ans)
	{
		if (!userList.contains(user))
		{
			System.out.println("User not found!");
			return;
		}
		if (!blogRepository.getAll().contains(blog))
		{
			System.out.println("Blog not found!");
			return;
		}
		if (ans.equalsIgnoreCase("y"))
		{
			blog.setBlogStatus(BlogStatus.PUBLISHED);
			System.out.println(blog.getTitle()+" is now published.");
		}
		user.getBlogs().add(blog);
	}

	public void deleteBlog(User user, Blog blog)
	{
		if (!userList.contains(user))
		{
			System.out.println("User not found!");
			return;
		}
		if (!blogRepository.getAll().contains(blog))
		{
			System.out.println("Blog not found!");
			return;
		}
		user.getBlogs().remove(blog);
		
	}

}
