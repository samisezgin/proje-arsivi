package emlakcepte.service;

import java.util.List;

import emlakcepte.dao.UserDao;
import emlakcepte.model.Search;
import emlakcepte.model.User;
import interfaces.IUserService;

public class UserService implements IUserService
{
	private UserDao userDao = new UserDao();
	
	public void createUser(User user)
	{
		//System.out.println(userDao);		
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
