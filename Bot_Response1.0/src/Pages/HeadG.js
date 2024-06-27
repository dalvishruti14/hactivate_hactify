import React from 'react';
import styled from 'styled-components';
import logo from '../images/image.png';
import { Link } from 'react-router-dom';

const HeaderWrapper = styled.header`
  background-color: #F5D2D2;
  color: white;
  //padding: 0px;
  z-index: 1000;
//position: fixed;
  width: 100%;
`;

const FlexContainer = styled.div`
  display: flex;
  align-items: center;
`;

const Nav = styled.nav`
  display: flex;
  justify-content: space-between;
  align-items: center;

  ul {
    list-style-type: none;
    padding: 0;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    margin-right: 16px;
  }

  li {
    margin: 0 1rem;
    cursor: pointer;
    color: #EF6968;
    transition: color 0.3s ease; /* Add transition effect */
  }

  a {
    text-decoration: none;
    color: #EF6968;
    transition: color 0.3s ease; /* Add transition effect */
  }

  li:hover,
  a:hover {
    color: #fff; /* Change color on hover */
  }
`;

const Name = styled.h1`
  margin-left: 10px;
  color: #000000;
  font-family: 'Playfair Display', serif;
  font-size: 30px;
`;

const Logo = styled.img`
  height: 90px;
  margin-right: 3px;
  margin-left: 19px;
`;

const Header = () => {
  const user = localStorage.getItem('user');
  const signOut = () => {
    localStorage.clear()
    window.location.reload()
};
  return (
    <HeaderWrapper>
      <Nav>
      <Link to='/'>
        <FlexContainer>
          <Logo src={logo} alt="Logo" />
          <Name>Sensory Learn</Name>
        </FlexContainer>
      </Link>
        <ul>
          {/* <li><Link to='/home'>Home</Link></li>SensoryLearn1/src/HeroSection.css SensoryLearn1/src/HeroSection.js SensoryLearn1/src/Home.js SensoryLearn1/src/HomeData.js */}
          <li><Link to='/subjects'>Subjects</Link></li>
          <li><Link to='/ask-doubts'>Ask Doubts</Link></li>
          <li><Link to='/ask-doubts'>Visualize</Link></li>
          {user ? <li onClick={signOut}>Sign Out</li> : <li><Link to='/signin'>Login</Link></li>}
        </ul>
      </Nav>
    </HeaderWrapper>
  );
};

export default Header;
