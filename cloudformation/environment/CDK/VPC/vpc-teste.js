"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
exports.__esModule = true;
exports.MyVpcStack = void 0;
var cdk = require("@aws-cdk/core");
var ec2 = require("@aws-cdk/aws-ec2");
var MyVpcStack = /** @class */ (function (_super) {
    __extends(MyVpcStack, _super);
    function MyVpcStack(scope, id, props) {
        var _this = _super.call(this, scope, id, props) || this;
        // Criando a VPC
        var vpc = new ec2.Vpc(_this, 'MyVpc', {
            cidr: '10.0.0.0/16',
            maxAzs: 2,
            subnetConfiguration: [
                {
                    cidrMask: 24,
                    name: 'PublicSubnet',
                    subnetType: ec2.SubnetType.PUBLIC
                },
                {
                    cidrMask: 24,
                    name: 'PrivateSubnet',
                    subnetType: ec2.SubnetType.PRIVATE
                },
            ]
        });
        // Saída do ID da VPC
        new cdk.CfnOutput(_this, 'VpcId', {
            value: vpc.vpcId
        });
        return _this;
    }
    return MyVpcStack;
}(cdk.Stack));
exports.MyVpcStack = MyVpcStack;
// Instanciando a stack CDK
var app = new cdk.App();
new MyVpcStack(app, 'MyVpcStack');
