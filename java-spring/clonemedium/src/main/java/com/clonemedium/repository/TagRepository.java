package com.clonemedium.repository;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Repository;

import com.clonemedium.model.Tag;

@Repository
public class TagRepository
{
	private static List<Tag> tagList = new ArrayList<Tag>();

	public void createTag(Tag tag)
	{
		tag.getBlogs().forEach(blog->blog.setTag(tag));
		tagList.add(tag);
	}

	public List<Tag> getAll()
	{
		return tagList;
	}

	public void removeTag(Tag tag)
	{
		if(!tagList.contains(tag))
		{
			System.out.println("The tag you want to remove is not exist! -"+tag.getTagName());
			return;
		}
		tag.getBlogs().forEach(blog->blog.setTag(null));
		tagList.remove(tag);
		
	}
	
	

}
