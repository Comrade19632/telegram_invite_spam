import React from "react";
import { Link, useNavigate } from "react-router-dom";
import Button from "../../common/Button";
import style from "./Header.module.sass";

export const Header = () => {
    const navigate = useNavigate()
    return (
        <div className={ style.container }>
            <div className={style.thumbnail}>
                <h1>money</h1>
                <Link 
                    to="#"
                    >наш telegram канал
                </Link>
            </div>
            <div className={style.buttons}>
                <Button 
                    onClick={()=>{navigate("/")} }   
                    name="главная"/>
                <Button 
                    onClick={()=>{alert("рассылка по каналам!")} }name="рассылка по каналам"/>
            </div>
        </div>
    )
}
