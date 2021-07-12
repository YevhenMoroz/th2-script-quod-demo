U
    �פ`�  �                   @   s   d dl mZ G dd� d�ZdS )�    )�basic_custom_actionsc                   @   sV   e Zd Zddd�Zdd� Zdd� Zdd	� Zd
d� Zdd� Zdd� Z	dd� Z
dd� ZdS )�
FixMessage� c                 C   s
   || _ d S �N��
parameters)�selfr   � r	   �Oc:\Users\srublyov\Desktop\P\th2-script-quod-demo\quod_qa\wrapper\fix_message.py�__init__   s    zFixMessage.__init__c                 C   s   | j S r   r   �r   r	   r	   r
   �get_parameters	   s    zFixMessage.get_parametersc                 C   s   || j |< d S r   r   )r   �parametr_nameZnew_parametr_valuer	   r	   r
   �change_parameter   s    zFixMessage.change_parameterc                 C   s   |D ]}|| | j |< qd S r   r   )r   Zparameter_list�keyr	   r	   r
   �change_parameters   s    zFixMessage.change_parametersc                 C   s
   | j | S r   r   )r   r   r	   r	   r
   �get_parameter   s    zFixMessage.get_parameterc                 C   s   | j �|� d S r   )r   �update)r   Z	parameterr	   r	   r
   �add_tag   s    zFixMessage.add_tagc                 C   s   | j �|� d S r   )r   �pop)r   Zparameter_namer	   r	   r
   �
remove_tag   s    zFixMessage.remove_tagc                 C   s
   | j d S )N�ClOrdIDr   r   r	   r	   r
   �get_ClOrdID   s    zFixMessage.get_ClOrdIDc                 C   s   | j �dt�d�i� d S )Nr   �	   )r   r   �bca�client_orderidr   r	   r	   r
   �add_random_ClOrdID   s    zFixMessage.add_random_ClOrdIDN)r   )�__name__�
__module__�__qualname__r   r   r   r   r   r   r   r   r   r	   r	   r	   r
   r      s   
r   N)�customr   r   r   r	   r	   r	   r
   �<module>   s   