import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';

export class MyVpcStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Criando a VPC
    const vpc = new ec2.Vpc(this, 'MyVpc', {
      cidr: '10.0.0.0/16', // CIDR block da VPC
      maxAzs: 2, // Número máximo de zonas de disponibilidade
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: 'PublicSubnet',
          subnetType: ec2.SubnetType.PUBLIC, // Subnet pública
        },
        {
          cidrMask: 24,
          name: 'PrivateSubnet',
          subnetType: ec2.SubnetType.PRIVATE, // Subnet privada
        },
      ],
    });

    // Saída do ID da VPC
    new cdk.CfnOutput(this, 'VpcId', {
      value: vpc.vpcId,
    });
  }
}

// Instanciando a stack CDK
const app = new cdk.App();
new MyVpcStack(app, 'MyVpcStack');
