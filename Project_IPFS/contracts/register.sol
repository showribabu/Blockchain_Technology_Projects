// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract register {
 
address[] _usernames;
uint[] _passwords;

mapping (address=> bool)  _users;



function signup(address username,uint password) public{
require(!_users[username]);
_usernames.push(username);
_passwords.push(password);
_users[username] = true;

}

function login(address username,uint password) public view returns(bool){

require(_users[username]);

for(uint i=0;i<_usernames.length;i++)
{
  if(_usernames[i]==username && _passwords[i]==password)
  {
    return true;
  }
}

return false;

}

function viewusers() public view returns(address[] memory,uint[] memory){

return(_usernames,_passwords);

}

}
