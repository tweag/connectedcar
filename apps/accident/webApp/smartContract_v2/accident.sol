pragma solidity ^0.4.24;

// import "stringUtils.sol";

contract accident {

  struct accidentType{
      uint counter;
      uint acceleration;
      uint latitude;
      uint longitude;
  }

  mapping (bytes32 => string) public notesReceived;

  accidentType accidentInfo;
  bytes32[] public personList;

  constructor(bytes32[] personNames , uint counterValue , uint accelerationValue , uint latitudeValue , uint longitudeValue) public {
      personList = personNames;
      accidentInfo.counter = counterValue;
      accidentInfo.acceleration = accelerationValue;
      accidentInfo.latitude = latitudeValue;
      accidentInfo.longitude = longitudeValue;
      for(uint i = 0; i < personList.length; i++) {
        notesReceived[ personList[i] ] = "NOT AGREE";
      }
  }

  function getPersonList() public view returns (bytes32[]) {
    return personList;
  }

  function getLatitude() public view returns (uint) {
    return accidentInfo.latitude;
  }

  function getLongitude() public view returns (uint) {
    return accidentInfo.longitude;
  }

  function validPerson(bytes32 person) public view returns (bool) {
    for(uint i = 0; i < personList.length; i++) {
      if (personList[i] == person) {return true;}
    }
    return false;
  }

  function agreeByPerson(bytes32 person) public {
    require(validPerson(person) == true);
    notesReceived[person] = "AGREE";
  }

  function notesFor(bytes32 person) public view returns (string) {
    require(validPerson(person) == true);
    return notesReceived[person];
    // return "AGREE";
  }


  function isFinalised() public view returns (bool) {
    for(uint i = 0; i < personList.length; i++) {
      if ( equal (notesReceived[ personList[i] ] , "NOT AGREE") ) {return false;}
    }
    return true;
  }

  function compare(string _a, string _b) internal returns (int) {
      bytes memory a = bytes(_a);
      bytes memory b = bytes(_b);
      uint minLength = a.length;
      if (b.length < minLength) minLength = b.length;
      //@todo unroll the loop into increments of 32 and do full 32 byte comparisons
      for (uint i = 0; i < minLength; i ++)
          if (a[i] < b[i])
              return -1;
          else if (a[i] > b[i])
              return 1;
      if (a.length < b.length)
          return -1;
      else if (a.length > b.length)
          return 1;
      else
          return 0;
  }
  /// @dev Compares two strings and returns true iff they are equal.
  function equal(string _a, string _b) internal returns (bool) {
      return compare(_a, _b) == 0;
  }


}
