#pragma once
#include <fstream>
#include <iostream>
#include <string>
#include <chrono>

class logger
{
public:
	logger(int id) : _id(id)
	{
		_log_file.open("C:\\tmp\\prime\\" + std::to_string(_id) + "_log.txt");
		info(" started!..");
	}

	void info(std::string msg)
	{
		if (_log_file.is_open())
		{
			std::cout << _id << msg;
			_log_file << _id << msg;
		}
		else 
		{
			std::cout << _id << " file is closed!";
		}
	}

private:
	int _id;
	std::ofstream _log_file;
};