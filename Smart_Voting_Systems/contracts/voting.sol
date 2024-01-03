// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract voting {
  
// take how many members are stand for lection..
uint[3]  public _votes=[0,0,0];

//mapping for check the voted or not..

mapping(address => bool) public voter;


function votecast(address wallet,uint id) public
{

require(!voter[wallet]);
  if(id==1)
  {
    _votes[0]+=1;

  }
  else if(id==2)
  {
    _votes[1]+=1;
  }
  else if(id==3)
  {
    _votes[2] +=1;

  }

  voter[wallet]=true;


}

function result() public view returns(uint[3] memory)
{
  return (_votes);
}



}
