import React from 'react';
import styled from 'styled-components';

const StyledFooter = styled.footer`
  background-color: #F5D2D2;
  padding: 20px;
  text-align: center;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
`;

const FooterColumns = styled.div`
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  margin-left: 10%;
`;

const Column = styled.div`
  flex: 1;
  margin: 10px;
  text-align: left;
  padding-left: 20px;

  ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
`;

const ColumnTitle = styled.h4`
  margin-bottom: 10px;
  position: relative;

  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    background-color: #333;
  }
`;

const StyledLink = styled.a`
  color: #555;
  text-decoration: none;
  transition: color 0.3s ease;
  font-weight: 600; /* Increase font weight */

  &:hover {
    color: #333;
    text-decoration: underline;
  }
`;

const SocialIcons = styled.ul`
  list-style: none;
  margin: 0;
  padding: 0;
`;

const SocialIconItem = styled.li`
  display: inline-block;
  margin-right: 10px;
`;

const SocialLink = styled.a`
  color: #333;
  text-decoration: none;
  font-size: 18px;
`;

const Text = styled.p`
transition: color 0.3s ease;
  font-weight: 600;
`;

const Footer = () => {
  return (
    <StyledFooter>
      <FooterColumns>
        <Column>
          <ColumnTitle>Made For</ColumnTitle>
          <Text>Google Solution Challenge 2024</Text>
          {/* Add more company information if needed */}
        </Column>

        <Column>
          <ColumnTitle>Quick Links</ColumnTitle>
          <ul>
            <li><StyledLink href="#">Home</StyledLink></li>
            <li><StyledLink href="#">About Us</StyledLink></li>
            <li><StyledLink href="#">Contact</StyledLink></li>
            {/* Add more styled links as needed */}
          </ul>
        </Column>

        <Column>
          <ColumnTitle>Connect with Us</ColumnTitle>
          <SocialIcons>
            <SocialIconItem>
              <SocialLink href="#"><i className="fab fa-facebook"></i></SocialLink>
            </SocialIconItem>
            <SocialIconItem>
              <SocialLink href="#"><i className="fab fa-twitter"></i></SocialLink>
            </SocialIconItem>
            <SocialIconItem>
              <SocialLink href="#"><i className="fab fa-linkedin"></i></SocialLink>
            </SocialIconItem>
            {/* Add more social media links as needed */}
          </SocialIcons>
        </Column>
      </FooterColumns>
    </StyledFooter>
  );
};

export default Footer;
