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
			<div>
				<img
					src={user.picture}
					alt="Profile"
					style={{
						borderRadius: "50%",
						margin: "auto"
					}}
				/>
				<h2>{user.name}</h2>
				<p className="lead text-muted">{user.email}</p>
			</div>
		</div>
	)
}

export default Profile