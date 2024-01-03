// SPDX-License-Identifier: MIT
pragma solidity  0.8.19;

contract file {

address[] _owners;
string[] _files;

mapping(string =>bool) _f;

function uploadfile(address owner,string memory filehash) public{

require(!_f[filehash]);

_owners.push(owner);
_files.push(filehash);

_f[filehash] = true;


}

function viewfiles() public view returns(address[] memory,string[] memory)
{

  return (_owners,_files);
}


}
