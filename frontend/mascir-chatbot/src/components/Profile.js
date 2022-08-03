import React from 'react'
import { useAuth0 } from '@auth0/auth0-react';

const Profile = () => {
	const { user } = useAuth0();

	return (
		<div style={{
			display: "grid",
			justifyContent: "center",
			alignItems: "center",
			textAlign: "center",
			height: "100%"
		}} >
			<div style={{
				color: "white"
			}}>
				<img
					src={user.picture}
					alt="Profile"
					style={{
						borderRadius: "50%",
						margin: "auto"
					}}
				/>
				<h2>Welcome {user.name} !</h2>
				<p className="lead text-muted">email: {user.email}</p>
			</div>
		</div>
	)
}

export default Profile