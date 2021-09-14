U
    �٤`�  �                   @   s6   d dl mZ d dlmZ d dlmZ G dd� d�ZdS )�    )�basic_custom_actions)�Stubs)�	Directionc                   @   sz   e Zd Zdd� Zddgdddfdd	�Zddgd
fdd�Zdgdddfdd�Zdgdddfdd�Zddgdddfdd�ZdS )�FixVerifierc                 C   s   t j| _|| _|| _d S )N)r   �verifier�TraderConnectivity�case_id)�selfr   r   � r
   �Pc:\Users\srublyov\Desktop\P\th2-script-quod-demo\quod_qa\wrapper\fix_verifier.py�__init__   s    zFixVerifier.__init__�ClOrdID�	OrdStatuszCheck ExecutionReport�FIRSTNc                 C   sB   |d kr| j }| j�t�|t�d||�|j| j|t�	|��� d S )NZExecutionReport�
r   r   �submitCheckRule�bca�create_check_rule�filter_to_grpc�checkpoint_idr   r   �Value�r	   �
parameters�response�key_parameters�message_name�	direction�caser
   r
   r   �CheckExecutionReport   s    ��z FixVerifier.CheckExecutionReportzCheck Rejectc              
   C   s.   | j �t�|t�d||�|j| j| j�� d S )N�Reject)r   r   r   r   r   r   r   r   )r	   r   r   r   r   r
   r
   r   �CheckReject   s    ��zFixVerifier.CheckRejectzCheck NewOrderSinglec                 C   sB   |d kr| j }| j�t�|t�d||�|j| j|t�	|��� d S )N�NewOrderSingler   r   r
   r
   r   �CheckNewOrderSingle&   s    ��zFixVerifier.CheckNewOrderSingle�OrigClOrdIDzCheck OrderCancelReplaceRequestc                 C   sB   |d kr| j }| j�t�|t�d||�|j| j|t�	|��� d S )N�OrderCancelReplaceRequestr   �r	   r   r   r   r   r   r   r
   r
   r   �CheckOrderCancelReplaceRequest5   s    ��z*FixVerifier.CheckOrderCancelReplaceRequestzCheck OrderCancelRequestc                 C   sB   |d kr| j }| j�t�|t�d||�|j| j|t�	|��� d S )N�OrderCancelRequestr   r%   r
   r
   r   �CheckOrderCancelRequestF   s    ��z#FixVerifier.CheckOrderCancelRequest)	�__name__�
__module__�__qualname__r   r   r    r"   r&   r(   r
   r
   r
   r   r      s   r   N)�customr   r   �stubsr   Zth2_grpc_common.common_pb2r   r   r
   r
   r
   r   �<module>   s   