import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import Logout from '@mui/icons-material/Logout';
import PersonIcon from '@mui/icons-material/Person';
import HomeIcon from '@mui/icons-material/Home';
import ChatIcon from '@mui/icons-material/Chat';
import { Link } from "react-router-dom";
import logo from "../assets/mascir-logo.jpg"

const Navbar = () => {
  // const {
  //   user,
  //   isAuthenticated,
  //   loginWithRedirect,
  //   logout,
  // } = useAuth0();
  const isAuthenticated = true;

  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);

  const logoutWithRedirect = () => {
    // logout({
    //   returnTo: window.location.origin,
    // });
  }

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <div className="navbar">
      <div className="logo">
        <img src={logo} alt="logo" style={{
          maxWidth: "100%",
          maxHeight: "100%"
        }}></img>
      </div>
      <div className="navlist">
        <ul>
          {/* {!isAuthenticated && (
            <li className="nav-element" onClick={() => loginWithRedirect()}>Login</li>
          )} */}
          {isAuthenticated && (
            <>
              <Tooltip title="Account settings">
                <IconButton
                  onClick={handleClick}
                  size="small"
                  aria-controls={open ? 'account-menu' : undefined}
                  aria-haspopup="true"
                  aria-expanded={open ? 'true' : undefined}
                >
                  <img
                    // src={user.picture || "https://cdn-icons-png.flaticon.com/512/1250/1250689.png"}
                    src="https://cdn-icons-png.flaticon.com/512/1250/1250689.png"
                    alt="Profile"
                    className="nav-user-profile rounded-circle"
                    width="50" style={{
                      borderRadius: "50%",
                      margin: "1rem",
                      border: "1px solid black",
                      width: "3rem",
                      height: "3rem"
                    }} />
                </IconButton>
              </Tooltip>
              <Menu
                anchorEl={anchorEl}
                id="account-menu"
                open={open}
                onClose={handleClose}
                onClick={handleClose}
                PaperProps={{
                  elevation: 0,
                  sx: {
                    overflow: 'visible',
                    filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
                    mt: 1.5,
                    '& .MuiAvatar-root': {
                      width: 32,
                      height: 32,
                      ml: -0.5,
                      mr: 1,
                    },
                    '&:before': {
                      content: '""',
                      display: 'block',
                      position: 'absolute',
                      top: 0,
                      right: 14,
                      width: 10,
                      height: 10,
                      bgcolor: 'background.paper',
                      transform: 'translateY(-50%) rotate(45deg)',
                      zIndex: 0,
                    },
                  },
                }}
                transformOrigin={{ horizontal: 'right', vertical: 'top' }}
                anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
              >
                <MenuItem>
                  <ListItemIcon>
                    <HomeIcon fontSize="small" />
                  </ListItemIcon>
                  <Link to="/">Home</Link>
                </MenuItem>
                <MenuItem>
                  <ListItemIcon>
                    <PersonIcon fontSize="small" />
                  </ListItemIcon>
                  <Link to="/profile">Profile</Link>
                </MenuItem>
                <MenuItem>
                  <ListItemIcon>
                    <ChatIcon fontSize="small" />
                  </ListItemIcon>
                  <Link to="/chatbot">Chat</Link>
                </MenuItem>
                <Divider />
                <MenuItem onClick={() => logoutWithRedirect()}>
                  <ListItemIcon>
                    <Logout fontSize="small" />
                  </ListItemIcon>
                  Logout
                </MenuItem>
              </Menu>
            </>
          )}
        </ul>
      </div>
    </div >
  );
};

export default Navbar;
