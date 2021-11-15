import React from "react"
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Container from 'react-bootstrap/Container';
import './Header.css';
import { Link } from "react-router-dom";


function Header() {
    return (
       <div className = 'page'>
           {/* From https://react-bootstrap.github.io/components/navbar/ */}
           <Navbar className="header header-container" expand="lg">
                <Container style={{}}>
                    <Link to="/" 
                        style={{color: '#ed1b76', textDecoration: 'unset', fontSize: '20px', marginRight: '10px'}}
                    >
                        Squad Game
                    </Link>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav" style={{color: 'white'}}>
                    <Nav className="me-auto">
                        <Nav.Link href="#home">Home</Nav.Link>
                        <Nav.Link href="#link">Events</Nav.Link>
                        <NavDropdown title="Additional Features" id="basic-nav-dropdown">
                        <NavDropdown.Item href="#action/3.1">Equipments</NavDropdown.Item>
                        <NavDropdown.Divider />
                        <NavDropdown.Item href="#action/3.2">Badges</NavDropdown.Item>
                        </NavDropdown>
                    </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
       </div>
    )
}

export default Header;