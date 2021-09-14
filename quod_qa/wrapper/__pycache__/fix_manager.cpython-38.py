U
    �͛`=  �                   @   sB   d dl mZ d dlmZ d dlmZ d dlmZ G dd� d�Z	dS )�    )�basic_custom_actions)�Stubs)�RequestMDRefID)�ConnectionIDc                   @   s`   e Zd Zdd� Zdd� Zddd�Zdd
d�Zddd�Zddd�Zddd�Z	ddd�Z
dd� ZdS ) �
FixManagerc                 C   s    || _ || _tj| _tj| _d S �N)�TraderConnectivity�case_idr   �fix_act�act�	simulator)�selfr   r	   � r   �Oc:\Users\srublyov\Desktop\P\th2-script-quod-demo\quod_qa\wrapper\fix_manager.py�__init__	   s    zFixManager.__init__c                 C   s   | j S r   )r	   )r   r   r   r   �get_case_id   s    zFixManager.get_case_id�Send NewOrderSingleNc                 C   s>   |d kr| j }| jjt�|| j|t�d|�� | j��d�}|S )NZNewOrderSingle��request)r	   r   �placeOrderFIX�bca�convert_to_requestr   �message_to_grpc�get_parameters�r   �fix_message�message_nameZcase�responser   r   r   �Send_NewOrderSingle_FixMessage   s    ��z)FixManager.Send_NewOrderSingle_FixMessage�Cancel orderc                 C   s>   |d kr| j }| jjt�|| j|t�d|�� | j��d�}|S )NZOrderCancelRequestr   �r	   r   �sendMessager   r   r   r   r   r   r   r   r   �"Send_OrderCancelRequest_FixMessage"   s    ��z-FixManager.Send_OrderCancelRequest_FixMessage�Replace orderc                 C   s>   |d kr| j }| jjt�|| j|t�d|�� | j��d�}|S )NZOrderCancelReplaceRequestr   r    r   r   r   r   �)Send_OrderCancelReplaceRequest_FixMessage/   s    ��z4FixManager.Send_OrderCancelReplaceRequest_FixMessage�Send MarketDatac                 C   sd   | j jtt|�t| jd�d�d�j}|�d|i� | jj	t
�|| j| jt
�d|�� | j��d�}|S )N��session_alias��symbol�connection_idr   �MDReqIDZMarketDataSnapshotFullRefresh)r   �getMDRefIDForConnectionr   �strr   r   �MDRefID�add_tagr   r!   r   r   r	   r   r   �r   r   r)   r   r+   r   r   r   r   �-Send_MarketDataFullSnapshotRefresh_FixMessage<   s    
���z8FixManager.Send_MarketDataFullSnapshotRefresh_FixMessage�Send Incremental MarketDatac                 C   s`   | j jt|t| jd�d�d�j}|�d|i� | jjt	�
|| j| jt	�d|�� | j��d�}|S )Nr&   r(   r   r+   ZMarketDataIncrementalRefresh)r   r,   r   r   r   r.   r/   r   r!   r   r   r	   r   r   r0   r   r   r   �,Send_MarketDataIncrementalRefresh_FixMessageO   s    
���z7FixManager.Send_MarketDataIncrementalRefresh_FixMessage�Send MarketDataRequestc                 C   s2   | j jt�|| j| jt�d|�� | j��d�}|S )NZMarketDataRequestr   )r   r!   r   r   r   r	   r   r   )r   r   r   r   r   r   r   �!Send_MarketDataRequest_FixMessage^   s    ��z,FixManager.Send_MarketDataRequest_FixMessagec                 C   sN   t j}|jtt| jd�d�d�}|jD ]"}t|j|j	it
|j|j	i�� q&d S )Nr&   )r*   r   )r   r   �getAllMDRefIDr   r   r   �PairsMDRefID�printr)   r.   �type)r   ZMDSymbolr   Z
allMDRefID�ir   r   r   �CheckSubscriptionh   s    
�

zFixManager.CheckSubscription)r   N)r   N)r#   N)r%   )r2   )r4   )�__name__�
__module__�__qualname__r   r   r   r"   r$   r1   r3   r5   r;   r   r   r   r   r      s   






r   N)
�customr   r   �stubsr   �th2_grpc_sim_quod.sim_pb2r   Zth2_grpc_common.common_pb2r   r   r   r   r   r   �<module>   s   