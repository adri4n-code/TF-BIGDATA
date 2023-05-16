create schema Libreria char set utf8mb4;
use Libreria;

create table Usuario(
	Nombre varchar (50) primary key,
    Apellidos varchar (100),
    Correo varchar (100),
    Contraseña varchar(72)
    );
    
create table Editorial(
    NombreEditorial varchar (50)primary key
    );
create	table Autor(
    NombreyApellidosAutor varchar(50) primary key primary key
    );
    
create table Libro(
    NombreLibro varchar(50)primary key,
    Estilo ENUM('Ficción', 'Educación','Literatura') NOT NULL   
    );

