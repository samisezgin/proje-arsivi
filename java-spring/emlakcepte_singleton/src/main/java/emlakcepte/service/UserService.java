package emlakcepte.service;

import java.util.List;

import emlakcepte.dao.UserDao;
import emlakcepte.model.Search;
import emlakcepte.model.User;

public class UserService
{
	private static UserService instance=null;
	private UserDao userDao = new UserDao();
	
	private UserService()
	{
		
	}
	public static UserService getInstance()
	{
		if(instance==null)
		{
			instance=new UserService();
		}
		return instance;
	}
	public void createUser(User user)
	{
		//System.out.println(userDao);
		if (user.getPassword().length() < 8)
		{
			System.out.println("Password must be at least 8 characters!");
			return;
		}
		userDao.createUser(user);
	}

	public List<User> getAllUsers()
	{
		return userDao.getAllUsers();
	}

	public void printAllUsers()
	{
		getAllUsers().forEach(user -> System.out.println(user.getName()));
	}
	
	public void saveSearch(User user, Search search)
	{
		userDao.saveSearch(user, search);
	}
}
