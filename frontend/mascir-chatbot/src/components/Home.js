import React from 'react'
import { Link } from "react-router-dom";
import Button from '@mui/material/Button';


const Home = () => {
	return (
		<div className='chatbot no-scroll' style={{
			// backgroundColor: "red",
		}}>
			<div class="two alt-two" style={{
				paddingTop: '4rem',
				color: "white"
			}}>
				<h1>Mascir chatbot
					<span>A chatbot dedicated for elderly care</span>
				</h1>
				<div style={{
					color: "rgb(91, 97, 102)",
					fontSize: "18px",
					marginTop: "100px",
					textAlign: "justify"
				}}><p>
						elderly care chatbot, est AI assistant, dédié a prendre soin des personnes âgées et interagir avec eux, dans une maison de retraite, doté de plusieurs fonctionnalités que vous allez découvrir tout de suite.
					</p>
				</div>
				<div style={{
					display: "grid",
					padding: "2rem",
					paddingLeft: "8rem",
					paddingRight: "8rem"
				}}>
					<Button variant="contained" size='large' className="main-btn"><Link to="/chatbot">Start chatting</Link></Button>
				</div>
			</div>
		</div>
	)
}

export default Home