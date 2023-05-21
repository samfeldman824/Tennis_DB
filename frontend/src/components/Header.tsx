import React from "react";
import { useMatch, useResolvedPath } from "react-router-dom";
import '../styles.css'
import { Link } from "react-router-dom"

function Header() {
  return (
    <nav className="header">
        <Link to="/" className="site-title"> 
            Tennis Database
        </Link>

        <ul>
            <CustomLink to='/Home'>Home</CustomLink>
            <CustomLink to='/Players'>Players</CustomLink>
            <CustomLink to="/Leaderboard">Leaderboard</CustomLink>
            <CustomLink to="/Data">Data</CustomLink>
            <CustomLink to="/About">About</CustomLink>
            
            

        </ul>




    </nav>
  );
}

interface CustomLinkProps extends React.AnchorHTMLAttributes<HTMLAnchorElement> {
    to: string;
  }

function CustomLink({ to, children, ...props}: CustomLinkProps) {
    const resolvedPath = useResolvedPath(to)
    const isActive = useMatch({ path: resolvedPath.pathname, end: true})
    return (
        <li className={isActive ? "active" : ""}>
            <Link to={to} {...props}>{children}</Link> 
        </li>
    )
}


export default Header;
